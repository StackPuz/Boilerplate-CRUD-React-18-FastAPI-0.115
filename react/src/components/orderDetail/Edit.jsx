import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function OrderDetailEdit(props) {
  
  const [ orderDetail, setOrderDetail ] = useState({})
  const [ products, setProducts ] = useState([])
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.orderId, props.match.params.no ])
  
  function get() {
    return Service.edit(props.match.params.orderId, props.match.params.no).then(response => {
      setOrderDetail(response.data.orderDetail)
      setProducts(response.data.products)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function edit(e) {
    e.preventDefault()
    Service.edit(props.match.params.orderId, props.match.params.no, orderDetail).then(() => {
      props.history.push(Util.getRef('/orderDetail'))
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
    let data = { ...orderDetail }
    data[e.target.name] = e.target.value
    setOrderDetail(data)
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={edit}>
            <div className="row">
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_detail_order_id">Order Id</label>
                <input readOnly id="order_detail_order_id" name="order_id" className="form-control form-control-sm" onChange={onChange} value={orderDetail.order_id ?? '' } type="number" required />
                {errors.order_id && <span className="text-danger">{errors.order_id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_detail_no">No</label>
                <input readOnly id="order_detail_no" name="no" className="form-control form-control-sm" onChange={onChange} value={orderDetail.no ?? '' } type="number" required />
                {errors.no && <span className="text-danger">{errors.no}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_detail_product_id">Product</label>
                <select id="order_detail_product_id" name="product_id" className="form-select form-select-sm" onChange={onChange} value={orderDetail.product_id ?? '' } required>
                  <option></option>
                  {products.map((product, index) =>
                  <option key={index} value={product.id}>{product.name}</option>
                  )}
                </select>
                {errors.product_id && <span className="text-danger">{errors.product_id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_detail_qty">Qty</label>
                <input id="order_detail_qty" name="qty" className="form-control form-control-sm" onChange={onChange} value={orderDetail.qty ?? '' } type="number" required />
                {errors.qty && <span className="text-danger">{errors.qty}</span>}
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/orderDetail')}>Cancel</Link>
                <button className="btn btn-sm btn-primary">Submit</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}