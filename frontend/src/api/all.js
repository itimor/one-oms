import Request from '@/api/common'

// auth
import * as auths from '@/api/auths'
export const auth = auths

// systems
export const user = new Request('/sys/user/')
export const role = new Request('/sys/role/')
export const menu = new Request('/sys/menu/')

// domains
export const domain = new Request('/domain/domain/')
export const brand = new Request('/domain/project/')
export const cdn = new Request('/domain/cdn/')
export const ipool = new Request('/domain/ipool/')

// tools
export const auditlog = new Request('/tool/auditlog/')
export const simple = new Request('/tool/simple/')
