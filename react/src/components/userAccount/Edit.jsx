import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function UserAccountEdit(props) {
  
  const [ userAccount, setUserAccount ] = useState({})
  const [ userAccountUserRoles, setUserAccountUserRoles ] = useState([])
  const [ roles, setRoles ] = useState([])
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.id ])
  
  function get() {
    return Service.edit(props.match.params.id).then(response => {
      setUserAccount(response.data.userAccount)
      setUserAccountUserRoles(response.data.userAccountUserRoles)
      setRoles(response.data.roles)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function edit(e) {
    e.preventDefault()
    if (!Util.validateForm()) {
      return
    }
    userAccount.role_id = Array.from(document.querySelectorAll('[name="role_id"]:checked')).map(e => e.value)
    Service.edit(props.match.params.id, userAccount).then(() => {
      props.history.push(Util.getRef('/userAccount'))
    }).catch((e) => {
      if (e.response.data.errors) {
        setErrors(e.response.data.errors)
      }
      else {
        alert(e.response.data.message)
      }
    })
  }

  function onChange(e) {
    let data = { ...userAccount }
    data[e.target.name] = (e.target.type == 'checkbox'? e.target.checked : e.target.value)
    setUserAccount(data)
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={edit}>
            <div className="row">
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_id">Id</label>
                <input readOnly id="user_account_id" name="id" className="form-control form-control-sm" onChange={onChange} value={userAccount.id ?? '' } type="number" required />
                {errors.id && <span className="text-danger">{errors.id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_name">Name</label>
                <input id="user_account_name" name="name" className="form-control form-control-sm" onChange={onChange} value={userAccount.name ?? '' } required maxLength="50" />
                {errors.name && <span className="text-danger">{errors.name}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_email">Email</label>
                <input id="user_account_email" name="email" className="form-control form-control-sm" onChange={onChange} value={userAccount.email ?? '' } type="email" required maxLength="50" />
                {errors.email && <span className="text-danger">{errors.email}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_password">Password</label>
                <input id="user_account_password" name="password" className="form-control form-control-sm" onChange={onChange} value={userAccount.password ?? '' } type="password" placeholder="New password" maxLength="100" />
                {errors.password && <span className="text-danger">{errors.password}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_password2">Confirm password</label>
                <input data-match="user_account_password" id="user_account_password2" name="password2" className="form-control form-control-sm" type="password" placeholder="New password" maxLength="100" />
                {errors.password && <span className="text-danger">{errors.password}</span>}
              </div>
              <div className="form-check col-md-6 col-lg-4">
                <input id="user_account_active" name="active" className="form-check-input" type="checkbox" onChange={onChange} value="1" checked={userAccount.active ?? '' } />
                <label className="form-check-label" htmlFor="user_account_active">Active</label>
                {errors.active && <span className="text-danger">{errors.active}</span>}
              </div>
              <div className="col-12">
                <h6>
                </h6><label className="form-label">Roles</label>
                {roles.map((role, index) =>
                <div key={index} className="form-check">
                  <input id={`user_role_role_id${role.id}`} name="role_id" className="form-check-input" type="checkbox" value={role.id} defaultChecked={userAccountUserRoles.some(e=> e.role_id == role.id)}/>
                  <label className="form-check-label" htmlFor={`user_role_role_id${role.id}`}>{role.name}</label>
                </div>
                )}
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/userAccount')}>Cancel</Link>
                <button className="btn btn-sm btn-primary">Submit</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}