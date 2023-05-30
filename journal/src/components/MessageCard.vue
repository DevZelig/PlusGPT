<template>
  <div class="d-flex flex-row">
    <div :class="[message.from == 'user' ? 'me-auto' : 'ms-auto', 'd-flex flex-column']">
      <div :class="[CardClass,'d-flex']">
        <template v-if="message.isgptloading === true">
          <div class="spinner-border text-end mx-auto" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </template>
        <template v-else>
          {{ message.message }}
        </template>
      </div>
      <p :class="[message.from == 'user' ? 'text-start ms-3' : 'text-end me-3', ' text-secondary m-0 mt-1 smol']">

        <img :src="[user_icon]" v-if="message.from == 'user'" class="icon" alt="">
        {{ message.time }}
        <img :src="[gpt_icon]" v-if="message.from != 'user'" class="icon" alt="">
      </p>
    </div>
  </div>
</template>

<script>


export default {
  name: 'MessageCard',
  props: {
    message: Object
  },
  data() {
    return {
      CardClass: 'm-3 p-3 mb-0 border rounded-3 border-1',
      gpt_icon: 'https://static.vecteezy.com/system/resources/previews/021/495/996/original/chatgpt-openai-logo-icon-free-png.png',
      user_icon: 'https://icons.veryicon.com/png/o/miscellaneous/two-color-icon-library/user-286.png'
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.icon {
  max-height: 24px;
  max-width: 24px;
  object-fit: cover;
}

.smol {
  font-size: 12px;
}

h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
