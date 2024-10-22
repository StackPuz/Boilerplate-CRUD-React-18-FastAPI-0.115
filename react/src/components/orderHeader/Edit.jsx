import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function OrderHeaderEdit(props) {
  
  const [ orderHeader, setOrderHeader ] = useState({})
  const [ orderHeaderOrderDetails, setOrderHeaderOrderDetails ] = useState([])
  const [ customers, setCustomers ] = useState([])
  const [ errors, setErrors ] = useState({})
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.id ])
  
  function get() {
    return Service.edit(props.match.params.id).then(response => {
      setOrderHeader(response.data.orderHeader)
      setOrderHeaderOrderDetails(response.data.orderHeaderOrderDetails)
      setCustomers(response.data.customers)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function edit(e) {
    e.preventDefault()
    Service.edit(props.match.params.id, orderHeader).then(() => {
      props.history.push(Util.getRef('/orderHeader'))
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
    let data = { ...orderHeader }
    data[e.target.name] = e.target.value
    setOrderHeader(data)
  }

  return (
    <div className="container">
      <div className="row">
        <div className="col">
          <form method="post" onSubmit={edit}>
            <div className="row">
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_header_id">Id</label>
                <input readOnly id="order_header_id" name="id" className="form-control form-control-sm" onChange={onChange} value={orderHeader.id ?? '' } type="number" required />
                {errors.id && <span className="text-danger">{errors.id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_header_customer_id">Customer</label>
                <select id="order_header_customer_id" name="customer_id" className="form-select form-select-sm" onChange={onChange} value={orderHeader.customer_id ?? '' } required>
                  <option></option>
                  {customers.map((customer, index) =>
                  <option key={index} value={customer.id}>{customer.name}</option>
                  )}
                </select>
                {errors.customer_id && <span className="text-danger">{errors.customer_id}</span>}
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_header_order_date">Order Date</label>
                <input id="order_header_order_date" name="order_date" className="form-control form-control-sm" onChange={onChange} value={orderHeader.order_date ?? '' } data-type="date" autoComplete="off" required />
                {errors.order_date && <span className="text-danger">{errors.order_date}</span>}
              </div>
              <div className="col-12">
                <table className="table table-sm table-striped table-hover">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Product</th>
                      <th>Qty</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderHeaderOrderDetails.map((orderHeaderOrderDetail, index) =>
                    <tr key={index}>
                      <td className="text-center">{orderHeaderOrderDetail.no}</td>
                      <td>{orderHeaderOrderDetail.product_name}</td>
                      <td className="text-end">{orderHeaderOrderDetail.qty}</td>
                      <td className="text-center">
                        <Link className="btn btn-sm btn-primary" to={`/orderDetail/edit/${orderHeaderOrderDetail.order_id}/${orderHeaderOrderDetail.no}`} title="Edit"><i className="fa fa-pencil"></i></Link>
                        <Link className="btn btn-sm btn-danger" to={`/orderDetail/delete/${orderHeaderOrderDetail.order_id}/${orderHeaderOrderDetail.no}`} title="Delete"><i className="fa fa-times"></i></Link>
                      </td>
                    </tr>
                    )}
                  </tbody>
                </table>
                <Link className="btn btn-sm btn-primary" to={`/orderDetail/create?order_detail_order_id=${orderHeader.id}`}>Add</Link>
                <hr />
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/orderHeader')}>Cancel</Link>
                <button className="btn btn-sm btn-primary">Submit</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}