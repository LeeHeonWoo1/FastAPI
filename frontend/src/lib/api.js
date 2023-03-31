import qs from "qs"
import { access_token, username, is_login } from "./store"
import {get} from 'svelte/store'
import {push} from 'svelte-spa-router'

const fastapi=(operation, url, params, success_callback, failure_callback) => {
    let method = operation
    let content_type = 'application/json'
    let body = JSON.stringify(params)

    if(operation === 'login') {
      method = 'post'
      content_type = 'application/x-www-form-urlencoded'
      body = qs.stringify(params)
    }
  
    let _url = import.meta.env.VITE_SERVER_URL + url
    if (method === 'get'){
      _url += "?" + new URLSearchParams(params)
    }
  
    let options = {
      method: method,
      headers: {
        "Content-Type": content_type
      }
    }

    const _access_token = get(access_token)
    if (_access_token) {
      options.headers["Authorization"] = "Bearer " + _access_token
    }

    if (method !== 'get'){
      options['body'] = body
    }
  
    fetch(_url, options)
      .then(res => {
        if (res.status === 204){
          if(success_callback){
              success_callback()
          }
          return
        }
        res.json().then(json=>{
          if(res.status >= 200 && res.status < 300) {
            if(success_callback){
              success_callback(json)
            }
          }else if (operation !== 'login' && res.status === 401){
            access_token.set('')
            username.set('')
            is_login.set(false)
            alert("로그인이 필요한 서비스입니다. 로그인 화면으로 이동합니다.")
            push('/user-login')
          }else{
            if (failure_callback){
              failure_callback(json)
            }else{
              alert(JSON.stringify(json))
            }
          }
        }).catch(error => {
          alert(JSON.stringify(error))
        })
      })
  }
  
export default fastapi