import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function BrandCreate(props) {
  
  const [ brand, setBrand ] = useState({})
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    Util.initView(true)
  }, [])

  function create(e) {
    e.preventDefault()
    Service.create(brand).then(() => {
      props.history.push(Util.getRef('/brand'))
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
    let data = { ...brand }
    data[e.target.name] = e.target.value
    setBrand(data)
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={create}>
            <div className="row">
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="brand_name">Name</label>
                <input id="brand_name" name="name" className="form-control form-control-sm" onChange={onChange} value={brand.name ?? '' } required maxLength="50" />
                {errors.name && <span className="text-danger">{errors.name}</span>}
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/brand')}>Cancel</Link>
                <button className="btn btn-sm btn-primary">Submit</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}