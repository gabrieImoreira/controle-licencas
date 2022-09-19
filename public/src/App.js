import React, { useState, useContext } from "react";
import axios from "axios";
import { Alert } from 'reactstrap'
import useForceUpdate from 'use-force-update';
var token = '';
var first_time = 0

// var Login = () => {
//     const [email, setEmail] = useState("");
//     const [password, setPassword] = useState("");
//     var [token,] = useState("");
    
//     const submitLogin = (async () => {
//       const requestOptions = {
//         method: "POST",
//         headers: { "Content-Type": "application/x-www-form-urlencoded" },
//         body: { 
//           login: email,
//           password: password
//         }
//       };
  
//       const response = await axios.post("http://192.168.0.21:5000/login", 
//       { 
//         login: email,
//         password: password
//       }).catch(function (error) {
//         console.log('err:', error)
//         });
//       if (response.status === 200) {
//         token = response.data.access_token;
//       } else {
//         console.log('error')
//       }
//       console.log('value', token)

//       return token
//     });

//     const handleSubmit = (e) => {
//       e.preventDefault();
//       submitLogin();
//     };
    
//     return (
        
//       <div className="container">
//         <form className="box text-center" onSubmit={handleSubmit}>
//           <h3 className="title text-center">Login</h3>
//           <div className="field text-center mt-2">
//             <label className="label">Usuário</label>
//             <div className="control">
//               <input
//                 type="text"
//                 placeholder="Usuário"
//                 value={email}
//                 onChange={(e) => setEmail(e.target.value)}
//                 className="input"
//                 required
//               />
//             </div>
//           </div>
//           <div className="field text-center mt-2">
//             <label className="label">Senha</label>
//             <div className="control">
//               <input
//                 type="password"
//                 placeholder="Senha"
//                 value={password}
//                 onChange={(e) => setPassword(e.target.value)}
//                 className="input"
//                 required
//               />
//             </div>
//           </div>
//           {/* <ErrorMessage message={errorMessage} /> */}
//           <br />
//           <button className="button is-primary" type="submit">
//             Login
//           </button>
//         </form>
//       </div>
//     );
//   };

// axios.defaults.withCredentials = true;
class App extends React.Component {

    
    constructor(props) {
        super(props);
        this.state =
        {
            users: [],
            email: '',
            expiration_date: '',
            id: 0,
            email_login: '',
            email_password: '',
            token: '',
            message: {
                'text': '',
                'alert': ''
            }
        }
    }
    componentTeste(){
        return 0
    }
    componentDidMount() {
        if (this.state.token !== ''){
        axios.get("http://192.168.0.21:5000/users")
            .then((res) =>
                this.setState({
                    users: res.data.users,
                    email: '',
                    expiration_date: '',
                    id: 0
                })
            )
        }
    }

    emailchange = event => {
        this.setState({
            email: event.target.value
        })
    }

    datechange = event => {
        this.setState({
            expiration_date: event.target.value
        })
    }

    submit(event, id) {
        const headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
        event.preventDefault()
        if (id === 0) {
            console.log('entrou no if', id)
                axios.post('http://192.168.0.21:5000/users',
                {
                    "email": this.state.email,
                    "expiration_date": this.state.expiration_date
                })
                .then((response) => {
                    if (response.status === 200){
                        this.setState({
                            message: {
                                'text': 'Usuário cadastrado com sucesso!',
                                'alert': 'success'
                            }})
                    }
                    this.componentDidMount();
                })
                .catch(function (error) {
                    console.log('err:', error)
                });
        } else {
            axios.put(`http://192.168.0.21:5000/users/${id}`,
                {
                    "email": this.state.email,
                    "expiration_date": this.state.expiration_date
                })
                .then(() => {
                    this.setState({
                        message: {
                            'text': 'Usuário atualizado com sucesso!',
                            'alert': 'success'
                        }})
                    this.componentDidMount();
                })
                .catch(function (error) {
                    console.log('err:', error);
                });
        }
    }

    delete(id) {
        axios.delete(`http://192.168.0.21:5000/users/${id}`)
            .then(() => {
                this.setState({
                    message: {
                        'text': 'Usuário deletado com sucesso!',
                        'alert': 'danger'
                    }})
                this.componentDidMount()
            })
    }

    getone(id) {
        axios.get(`http://192.168.0.21:5000/users/${id}`)
            .then((res) => {
                this.setState({
                    email: res.data.email,
                    expiration_date: res.data.expiration_date,
                    id: res.data.id
                })
            })
    }

    setEmail = event => {
        this.setState({
            email_login: event.target.value
        })
    }

    setPassword = event => {
        this.setState({
            email_password: event.target.value
        })
    }

    submitLogin = () => {
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: { 
            login: this.state.email_login,
            password: this.state.email_password
          }
        }
        const response = axios.post("http://192.168.0.21:5000/login", 
          { 
            login: this.state.email_login,
            password: this.state.email_password
          })
          .then((response) => { 
            if (response.status === 200) {
                this.state.token = response.data.access_token
                this.render()
            }
          })   
          .catch(function (error) {
            console.log('err:', error)
            })
    
          
        // forceUpdate();
        
    };
    handleSubmit = (e) => {
        console.log(this.state.email_login)
        console.log(this.state.email_password)
        this.submitLogin();
        e.preventDefault();
        
    };
    render() {
        var page_login = <div className="container">
        <form className="box text-center" onSubmit={this.handleSubmit}>
          <h3 className="title text-center">Login</h3>
          <div className="field text-center mt-2">
            <label className="label">Usuário</label>
            <div className="control">
              <input
                type="text"
                placeholder="Usuário"
                value={this.state.email_login}
                onChange={(e) => this.setEmail(e)}
                className="input"
                required
              />
            </div>
          </div>
          <div className="field text-center mt-2">
            <label className="label">Senha</label>
            <div className="control">
              <input
                type="password"
                placeholder="Senha"
                value={this.state.email_password}
                onChange={(e) => this.setPassword(e)}
                className="input"
                required
              />
            </div>
          </div>
          {/* <ErrorMessage message={errorMessage} /> */}
          <br />
          <button className="button is-primary" type="submit">
            Login
          </button>
        </form>
      </div>
        
        var page_users = <div className="row mt-5">
                   
        <div className="mt-2">
            {
                this.state.message.text !== '' ? (
                    <Alert color={this.state.message.alert} className="text-center mt-2"> {this.state.message.text}</Alert>
                ) : ''
            }
        </div>
        <div className="col lg-6 mt-2">
            <form onSubmit={(e) => { this.submit(e, this.state.id) }}>
                <div className="form-group">
                    <input type="email" onChange={(e) => { this.emailchange(e) }} className="form-control mt-2" placeholder="E-mail" value={this.state.email} />
                </div>
                <div className="form-group">
                    <input type="date" onChange={(e) => { this.datechange(e) }} className="form-control mt-2" placeholder="Data de expiração" value={this.state.expiration_date} />
                </div>
                <button className="btn btn-block btn-primary mt-2">Enviar</button>
            </form>
        </div>
        <div className="col lg-6 mt-2">
            <table className="table">
                <thead>
                    <tr>
                        <th>E-mail</th>
                        <th>Data de expiração</th>
                        <th>Editar</th>
                        <th>Deletar</th>
                    </tr>
                </thead>
                <tbody>
  
                    {this.state.users.map(user =>
                        <tr>
                            <td>{user.email}</td>
                            <td>{user.expiration_date}</td>
                            <td>
                                <button onClick={(e) => this.getone(user.id)} className="btn btn-sm btn-primary">
                                    <i className="fa fa-pencil"></i>
                                </button>
                            </td>
                            <td>
                                <button onClick={(e) => this.delete(user.id)} className="btn btn-sm btn-danger">
                                    <i className="fa fa-trash"></i>
                                </button>
                            </td>
                        </tr>
  
                    )}
                </tbody>
            </table>
        </div>
  
  
    </div>
        
        if (this.state.token === ''){
            var page = page_login
        } else {
            first_time = first_time + 1
            var page = page_users
            if (first_time === 1){
                console.log(first_time)
            this.componentDidMount()
            }
        }

        return (
            <div className="container mt-5">
                 {page}
            </div>
        );
    }
}

export default App;
