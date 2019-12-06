import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/sys/jwt-token-auth/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/sys/getuserinfo/',
    method: 'get'
  })
}

export function logout(data) {
  return
}

export function changepwd(data) {
  return request({
    url: '/sys/changepwd/',
    method: 'post',
    data
  })
}

