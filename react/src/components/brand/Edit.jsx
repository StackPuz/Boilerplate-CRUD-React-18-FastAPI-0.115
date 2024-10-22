import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function BrandEdit(props) {
  
  const [ brand, setBrand ] = useState({})
  const [ brandProducts, setBrandProducts ] = useState([])
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.id ])
  
  function get() {
    return Service.edit(props.match.params.id).then(response => {
      setBrand(response.data.brand)
      setBrandProducts(response.data.brandProducts)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function edit(e) {
    e.preventDefault()
    Service.edit(props.match.params.id, brand).then(() => {
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
          <form method="post" onSubmit={edit}>
            <div className="row">
              <input type="hidden" id="brand_id" name="id" onChange={onChange} value={brand.id ?? '' } />
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="brand_name">Name</label>
                <input id="brand_name" name="name" className="form-control form-control-sm" onChange={onChange} value={brand.name ?? '' } required maxLength="50" />
                {errors.name && <span className="text-danger">{errors.name}</span>}
              </div>
              <div className="col-12">
                <h6>Brand's products</h6>
                <table className="table table-sm table-striped table-hover">
                  <thead>
                    <tr>
                      <th>Product Name</th>
                      <th>Price</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {brandProducts.map((brandProduct, index) =>
                    <tr key={index}>
                      <td>{brandProduct.name}</td>
                      <td className="text-end">{brandProduct.price}</td>
                      <td className="text-center">
                        <Link className="btn btn-sm btn-secondary" to={`/product/${brandProduct.id}`} title="View"><i className="fa fa-eye"></i></Link>
                        <Link className="btn btn-sm btn-primary" to={`/product/edit/${brandProduct.id}`} title="Edit"><i className="fa fa-pencil"></i></Link>
                        <Link className="btn btn-sm btn-danger" to={`/product/delete/${brandProduct.id}`} title="Delete"><i className="fa fa-times"></i></Link>
                      </td>
                    </tr>
                    )}
                  </tbody>
                </table>
                <Link className="btn btn-sm btn-primary" to={`/product/create?product_brand_id=${brand.id}`}>Add</Link>
                <hr />
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