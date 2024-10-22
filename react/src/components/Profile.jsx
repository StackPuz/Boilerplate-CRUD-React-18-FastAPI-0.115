import React, { useState, useEffect } from 'react'
import http from '../http'
import Util from '../util'

export default function Profile(props) {
  
  const [ userAccount, setUserAccount ] = useState({})
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [])
  
  function get() {
    return http.get('/profile').then(response => {
      setUserAccount(response.data.userAccount)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function edit(e) {
    e.preventDefault()
    if (!Util.validateForm()) {
      return
    }
    http.post('/updateProfile', userAccount).then(() => {
      props.history.push('/home')
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
    data[e.target.name] = e.target.value
    setUserAccount(data)
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={edit}>
            <div className="row">
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
              <div className="col-12">
                <button className="btn btn-sm btn-primary">Submit</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}