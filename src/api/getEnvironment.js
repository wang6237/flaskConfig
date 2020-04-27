import request from '@/utils/request'

export function getEnvLists() {
  return request({
    url: '/v1/env/',
    method: 'get'
  })
}

export function addEnvList(data) {
  return request({
    url: '/v1/env/',
    method: 'post',
    data
  })
}

export function editEnvList(id, data) {
  return request({
    url: '/v1/env/' + id,
    method: 'put',
    data
  })
}

export function delEnvList(id) {
  return request({
    url: '/v1/env/' + id,
    method: 'delete'
    // params: { name }
  })
}

export function syncEtcd(data) {
  return request({
    url: '/v1/env/sync/',
    method: 'post',
    data
  })
}

export function syncEtcdDelete(path, envId) {
  return request({
    url: '/v1/env/sync/',
    method: 'delete',
    params: { path, envId }
  })
}

export function syncState(data) {
  return request({
    url: '/v1/env/sync/state/',
    method: 'put',
    data
  })
}
