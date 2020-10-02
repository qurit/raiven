export const generic_get = async ({ $axios }, url, params) => (await $axios.get(url, params)).data

export const generic_post = async ({ $axios }, url, payload) => (await $axios.post(url, payload)).data

export const generic_delete = async ({ $axios }, url) => (await $axios.delete(url)).data


