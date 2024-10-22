import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function UserAccountDelete(props) {
  
  const [ userAccount, setUserAccount ] = useState({})
  const [ userAccountUserRoles, setUserAccountUserRoles ] = useState([])
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.id ])
  
  function get() {
    return Service.delete(props.match.params.id).then(response => {
      setUserAccount(response.data.userAccount)
      setUserAccountUserRoles(response.data.userAccountUserRoles)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function remove(e) {
    e.preventDefault()
    Service.delete(props.match.params.id, userAccount).then(() => {
      props.history.push(Util.getRef('/userAccount'))
    }).catch((e) => {
      alert(e.response.data.message)
    })
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={remove}>
            <div className="row">
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_id">Id</label>
                <input readOnly id="user_account_id" name="id" className="form-control form-control-sm" value={userAccount.id ?? '' } type="number" required />
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_name">Name</label>
                <input readOnly id="user_account_name" name="name" className="form-control form-control-sm" value={userAccount.name ?? '' } required maxLength="50" />
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="user_account_email">Email</label>
                <input readOnly id="user_account_email" name="email" className="form-control form-control-sm" value={userAccount.email ?? '' } type="email" required maxLength="50" />
              </div>
              <div className="form-check col-md-6 col-lg-4">
                <input readOnly id="user_account_active" name="active" className="form-check-input" type="checkbox" value="1" checked={userAccount.active ?? '' } />
                <label className="form-check-label" htmlFor="user_account_active">Active</label>
              </div>
              <div className="col-12">
                <h6>Roles</h6>
                <table className="table table-sm table-striped table-hover">
                  <thead>
                    <tr>
                      <th>Role Name</th>
                    </tr>
                  </thead>
                  <tbody>
                    {userAccountUserRoles.map((userAccountUserRole, index) =>
                    <tr key={index}>
                      <td>{userAccountUserRole.role_name}</td>
                    </tr>
                    )}
                  </tbody>
                </table>
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/userAccount')}>Cancel</Link>
                <button className="btn btn-sm btn-danger">Delete</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}