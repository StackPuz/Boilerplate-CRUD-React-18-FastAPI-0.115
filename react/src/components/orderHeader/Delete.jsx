import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Service from './Service'
import Util from '../../util'

export default function OrderHeaderDelete(props) {
  
  const [ orderHeader, setOrderHeader ] = useState({})
  const [ orderHeaderOrderDetails, setOrderHeaderOrderDetails ] = useState([])
  
  useEffect(() => {
    get().finally(() => {
      Util.initView(true)
    })
  }, [ props.match.params.id ])
  
  function get() {
    return Service.delete(props.match.params.id).then(response => {
      setOrderHeader(response.data.orderHeader)
      setOrderHeaderOrderDetails(response.data.orderHeaderOrderDetails)
    }).catch(e => {
      alert(e.response.data.message)
    })
  }

  function remove(e) {
    e.preventDefault()
    Service.delete(props.match.params.id, orderHeader).then(() => {
      props.history.push(Util.getRef('/orderHeader'))
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
                <label className="form-label" htmlFor="order_header_id">Id</label>
                <input readOnly id="order_header_id" name="id" className="form-control form-control-sm" value={orderHeader.id ?? '' } type="number" required />
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="customer_name">Customer</label>
                <input readOnly id="customer_name" name="customer_name" className="form-control form-control-sm" value={orderHeader.customer_name ?? '' } maxLength="50" />
              </div>
              <div className="mb-3 col-md-6 col-lg-4">
                <label className="form-label" htmlFor="order_header_order_date">Order Date</label>
                <input readOnly id="order_header_order_date" name="order_date" className="form-control form-control-sm" value={orderHeader.order_date ?? '' } data-type="date" autoComplete="off" required />
              </div>
              <div className="col-12">
                <table className="table table-sm table-striped table-hover">
                  <thead>
                    <tr>
                      <th>No</th>
                      <th>Product</th>
                      <th>Qty</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orderHeaderOrderDetails.map((orderHeaderOrderDetail, index) =>
                    <tr key={index}>
                      <td className="text-center">{orderHeaderOrderDetail.no}</td>
                      <td>{orderHeaderOrderDetail.product_name}</td>
                      <td className="text-end">{orderHeaderOrderDetail.qty}</td>
                    </tr>
                    )}
                  </tbody>
                </table>
              </div>
              <div className="col-12">
                <Link className="btn btn-sm btn-secondary" to={Util.getRef('/orderHeader')}>Cancel</Link>
                <button className="btn btn-sm btn-danger">Delete</button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}