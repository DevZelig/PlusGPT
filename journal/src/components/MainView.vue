<template>
  <div class="container-fluid d-flex flex-column vh-100">
    <div class="d-flex flex-column mt-auto overflow-auto" ref="scrollingDiv">
      <template v-for="(message, index) in messages" :key="index">
        <MessageCard :message="message" />
      </template>
    </div>


    <div class="row">
      <div class="input-group mb-5 mt-3">
        <input type="text" class="form-control" @keyup.enter="handleSubmit" v-model="inputValue"
          placeholder="Write your message here" aria-label="Username" aria-describedby="basic-addon1">
        <button type="button" class="btn btn-primary" @click="handleSubmit">Send message</button>
      </div>
    </div>
  </div>
</template>

<script>
import MessageCard from './MessageCard.vue'
import moment from 'moment'
import axios from 'axios';

export default {
  name: 'MainView',
  components: { MessageCard },
  data() {
    return {
      canMsg: true,
      messages: [
        {
          message: 'What is your thanks giving today? 😊',
          from: 'gpt',
          id: 1,
          time: this.formattedDate(),
          isgptloading: false
        }
      ],
      roles: [{
        content: 'You are a helper that encourages people to be grateful, you only reply within 100 tokens and prompts user 1 question after they talk about their day, you talk naturally,friendly, and sometimes include emojis',
        startingMessage: 'What is your thanks giving today? 😊'
      }, {
        content: 'You are a counselor that helps me feel better, you talk naturally, friendly, and sometimes include emojis',
        startingMessage: 'How are you feeling today? 😊'
      },{
        content: 'You are a trip advisor with a reply limit of 1000 tokens, you talk naturally, friendly, and include emojis appropriately',
        startingMessage: 'How may I help your adventurous needs? 😊'
      },
      ],
      cacheMessages: [
      { "role": "system", "content": 'You are a helper that encourages people to be grateful, you only reply within 100 tokens and prompts user 1 question after they talk about their day, you talk naturally,friendly, and sometimes include emojis' }
      ]
    }
  },
  methods: {
    getRoles() {
      var _t = []
      this.roles.forEach(role => {
        _t.push({ "role": "system", "content": role.content })
      })
      return _t
    },
    getRole(i) {
      return { "role": "system", "content": this.roles[i].content }
    },
    getMessage(i) {
      return this.roles[i].startingMessage
    },
    formattedDate() {
      return moment().format('DD/MM/YYYY hh:mm A')
    },
    handleSubmit() {
      if (!this.canMsg) {
        return
      }
      var msg = this.inputValue
      this.messages.push({
        message: msg,
        from: 'user',
        id: this.messages.length,
        time: this.formattedDate()
      })
      this.postToChatGpt()
      // console.log(this.messages)
      this.inputValue = '';
      this.$nextTick(() => {
        this.$refs.scrollingDiv.scrollTop = this.$refs.scrollingDiv.scrollHeight;
      });
    },
    getkey() {
      return process.env.GPTKEY
    },
    async postToChatGpt() {
      try {
        this.buildMessage()
        var messages = this.cacheMessages
        this.messages.push({
          message: 'tmp',
          from: 'gpt',
          id: this.messages.length,
          time: this.formattedDate(),
          isgptloading: true
        })


        const res = await axios.post('http://127.0.0.1:5001/prompt', {
          messages
        }, {
          headers: {
            'Content-Type': 'application/json',
          },
        });


        console.log(res.data)
        this.messages[this.messages.length - 1].message = res.data
        this.messages[this.messages.length - 1].isgptloading = false
      } catch (err) {
        console.error(err);
        this.messages[this.messages.length - 1].isgptloading = false
        this.messages[this.messages.length - 1].message = err
      }
    },
    buildMessage() {
      var _temp = [this.cacheMessages[0]]
      this.messages.forEach(message => {
        var msg = message.message
        var from = message.from
        var role
        if (from == 'gpt') {
          role = 'assistant'
        } else {
          role = 'user'
        }
        _temp.push({ "role": role, "content": msg })
      });
      this.cacheMessages = _temp
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
