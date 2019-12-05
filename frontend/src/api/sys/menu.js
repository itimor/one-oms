import request from '@/utils/request'

const apiurl = '/menu/'

export function requestPost(data) {
  return request({
    url: apiurl,
    method: 'post',
    data
  })
}

export function requestDelete(data) {
  return request({
    url: apiurl,
    method: 'delete',
    data
  })
}

export function requestPut(id, data) {
  return request({
    url: apiurl + id + '/',
    method: 'put',
    data
  })
}

export function requestGet(query) {
  return request({
    url: apiurl,
    method: 'get',
    params: query
  })
}

export function requestMenuButton(menucode) {
  return request({
    url: '/sys/getmenubutons',
    method: 'get',
    params: { menucode }
  })
}
