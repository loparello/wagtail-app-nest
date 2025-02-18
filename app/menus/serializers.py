import uuid

from django.db.models.query import QuerySet

from rest_framework import serializers

from wagtail.models import Page

from .helpers import (
    get_link_block_label,
    get_link_block_url,
    get_link_block_target,
    menu_item_page_is_active,
    menu_category_is_active,
    menu_category_has_submenu,
)
from .models import Menu


class MenuItemLinkSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    target = serializers.CharField(required=False, default="_self")


class BaseMenuItemSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    label = serializers.CharField(required=False, allow_blank=True)
    handle = serializers.CharField(required=False, allow_blank=True)
    active = serializers.BooleanField(default=False)
    link = MenuItemLinkSerializer(required=False)
    has_submenu = serializers.BooleanField(default=False)
    is_submenu_item = serializers.BooleanField(default=False)
    submenu_items = serializers.ListField(child=serializers.DictField(), required=False)

    def get_page_link_child_pages(self, page) -> QuerySet:
        return page.get_children().live().in_menu()

    def serialize_submenu_items(self, serializer_class, items, context) -> list[dict]:
        if isinstance(items, QuerySet):
            items = list(items)

        serializer = serializer_class(
            items,
            many=True,
            context=context,
        )
        return serializer.data


class BaseMenuItemBlockSerializer(BaseMenuItemSerializer):
    def get_active(self, block) -> bool:
        block_type = self.context.get("block_type")
        check_active_item = self.context.get("check_active_item")
        current_page = self.context.get("current_page")

        if not check_active_item:
            return False

        if block_type == "page_link":
            return menu_item_page_is_active(block.value.get("page"), current_page)
        elif block_type == "menu_category":
            return menu_category_is_active(block.value, current_page)

        return False

    def get_link(self, block) -> dict:
        block_type = self.context.get("block_type")

        if block_type in ["page_link", "url_link"]:
            serializer = MenuItemLinkSerializer(
                data={
                    "url": get_link_block_url(block.value),
                    "target": get_link_block_target(block.value),
                }
            )
            return serializer.validated_data if serializer.is_valid() else None

        return None

    def get_has_submenu(self, block) -> bool:
        block_type = self.context.get("block_type")

        if block_type == "page_link":
            if not block.value.get("add_submenu"):
                return False

            page_child_pages = self.context.get("page_child_pages")
            return page_child_pages.exists()
        elif block_type == "menu_category":
            return menu_category_has_submenu(block.value)

        return False

    def to_representation(self, block):
        block_dict = block.get_prep_value()
        block_type = block_dict["type"]
        self.context["block_dict"] = block_dict
        self.context["block_type"] = block_type

        if block_type == "page_link":
            page = block.value.get("page")
            self.context["page"] = page
            self.context["page_child_pages"] = self.get_page_link_child_pages(page)

        has_submenu = self.get_has_submenu(block)
        self.context["has_submenu"] = has_submenu

        return {
            "id": block_dict["id"],
            "type": block_type,
            "label": get_link_block_label(block.value),
            "handle": block.value["handle"],
            "active": self.get_active(block),
            "link": self.get_link(block),
            "has_submenu": has_submenu,
            "is_submenu_item": False,
            "submenu_items": [],
        }


class SubmenuPageItemSerializer(BaseMenuItemSerializer):
    def get_active(self, page) -> bool:
        check_active_item = self.context.get("check_active_item")
        current_page = self.context.get("current_page")

        if not check_active_item:
            return False

        return menu_item_page_is_active(page, current_page)

    def get_link(self, page) -> dict:
        request = self.context.get("request")
        serializer = MenuItemLinkSerializer(
            data={
                "url": page.get_url(request),
            }
        )
        return (
            serializer.validated_data
            if serializer.is_valid()
            else None
        )

    def get_has_submenu(self, page) -> bool:
        menu = self.context.get("menu")
        page_child_pages = self.context.get("page_child_pages")
        return page_child_pages.exists() and menu.submenu_levels == 2

    def get_submenu_items(self, page) -> list[dict]:
        if not self.context.get("has_submenu"):
            return []

        page_child_pages = self.context.get("page_child_pages")

        return self.serialize_submenu_items(
            SubmenuPageItemSerializer,
            page_child_pages,
            context=self.context,
        )

    def to_representation(self, page):
        self.context["page_child_pages"] = self.get_page_link_child_pages(page)
        has_submenu = self.get_has_submenu(page)
        self.context["has_submenu"] = has_submenu

        return {
            "id": str(uuid.uuid4()),
            "type": "page_link",
            "label": page.title,
            "handle": "",
            "active": self.get_active(page),
            "link": self.get_link(page),
            "has_submenu": has_submenu,
            "is_submenu_item": True,
            "submenu_items": self.get_submenu_items(page),
        }


class SubmenuItemBlockSerializer(BaseMenuItemBlockSerializer):
    def get_submenu_items(self, block) -> list[dict]:
        block_type = self.context.get("block_type")
        has_submenu = self.context.get("has_submenu")

        if block_type == "page_link" and has_submenu:
            page_child_pages = self.context.get("page_child_pages")
            return self.serialize_submenu_items(
                SubmenuPageItemSerializer,
                page_child_pages,
                context=self.context,
            )

        return []

    def to_representation(self, block):
        data = super().to_representation(block)
        data["is_submenu_item"] = True
        data["submenu_items"] = self.get_submenu_items(block)

        return data


class MenuItemBlockSerializer(BaseMenuItemBlockSerializer):
    def get_submenu_items(self, block) -> list[dict]:
        if not self.context.get("has_submenu"):
            return []

        block_type = self.context.get("block_type")

        if block_type == "page_link":
            page_child_pages = self.context.get("page_child_pages")
            return self.serialize_submenu_items(
                SubmenuPageItemSerializer,
                page_child_pages,
                context=self.context,
            )

        if block_type == "menu_category":
            submenu_items = block.value.get("submenu_items")
            return self.serialize_submenu_items(
                SubmenuItemBlockSerializer,
                submenu_items,
                context=self.context,
            )

        return []

    def to_representation(self, block):
        data = super().to_representation(block)
        data["submenu_items"] = self.get_submenu_items(block)

        return data


class MenuSerializer(serializers.ModelSerializer):
    menu_items = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = [
            "id",
            "title",
            "handle",
            "heading",
            "is_main",
            "menu_items",
        ]

    def get_menu_items(self, obj):
        serializer = MenuItemBlockSerializer(
            obj.menu_items,
            many=True,
            context={
                **self.context,
                "menu": obj,
            },
        )
        return serializer.data


def serialize_menu_to_dict(
    menu: Menu,
    request: object = None,
    current_page: Page = None,
    check_active_item: bool = False,
) -> dict:
    serializer = MenuSerializer(
        menu,
        context={
            "request": request,
            "current_page": current_page,
            "check_active_item": check_active_item,
        },
    )
    return serializer.data
