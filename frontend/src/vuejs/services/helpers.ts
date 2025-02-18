interface FormDataObject {
  [key: string]: string | Blob;
}

export function getFormData(object: FormDataObject): FormData {
  return Object.keys(object).reduce((formData: FormData, key: string) => {
    formData.append(key, object[key]);
    return formData;
  }, new FormData());
}
