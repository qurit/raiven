# Frontend

The frontend is built primarily using [Vue](https://vuejs.org/), [Vuetify](https://vuetifyjs.com/en/), and [Nuxt](https://nuxtjs.org/) in JavaScript.

## Pages

The pages directory contains the routes for the various pages of the application. You can modify the layour and appearance of a page in `\frontend\pages`, or simply add another page by creating a new file.

If you created a new page, you can also update the navigation drawer in `\frontend\layouts\default.vue `.

## Components

Components can be found under `\frontend\components` and are categorized and grouped together by their functionality. You can check the official [Vue Style Guide](https://vuejs.org/v2/style-guide/) to see how your components should be organized.

You can find a variety of Material Design ocons to use [here](https://materialdesignicons.com/)

## Store

The [Vuex store](https://vuex.vuejs.org/) pulls information from the backend and contains relevant information that can be used among other components in the project. You can modify the store in `\frontend\store`.

You can communicate with the backend using [axios](https://github.com/axios/axios), a promise based HTTP client. Generic requests have been implemented in `\frontend\api\index.js`.

## Images

If you would like to add or modify images, you can find them under `\frontend\static`.
