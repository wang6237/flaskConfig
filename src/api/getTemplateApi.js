import request from '@/utils/request'

// 获取etcd server 列表
export function getTemplateList() {
  return request({
    url: '/v1/template',
    method: 'get'
    // params: { page, limit }
  })
}

export function addTemplate(data) {
  return request({
    url: '/v1/template/',
    method: 'post',
    data
  })
}

export function editTemplate(data) {
  return request({
    url: '/v1/template/',
    method: 'put',
    data
  })
}

export function deleteTemplate(id) {
  return request({
    url: '/v1/template/' + id,
    method: 'delete'
    // params: { name }
  })
}

