import request from '@/utils/request'

const apiurl = '/workflow/'

export function requestPost(data) {
  return request({
    url: apiurl,
    method: 'post',
    data
  })
}

export function requestDelete(id) {
  return request({
    url: apiurl + id + '/',
    method: 'delete'
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
