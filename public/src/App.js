import React from "react";
import axios from "axios";
import { Alert } from 'reactstrap'

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
            message: {
                'text': '',
                'alert': ''
            }
        }
    }

    componentDidMount() {
        axios.get("http://192.168.0.21:5000/users")
            .then((res) =>
                this.setState({
                    users: res.data.users,
                    email: '',
                    expiration_date: '',
                    id: 0
                }, () => {
                    console.log(this.state.users);
                })
            )
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
            console.log('entrou no else', id)
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

    render() {
        return (

            <div className="container mt-5">

                <div className="row mt-5">
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
            </div>
        );
    }
}

export default App;
