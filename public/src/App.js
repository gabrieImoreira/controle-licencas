import React from "react";
import axios from "axios";

// axios.defaults.withCredentials = true;
class App extends React.Component {


constructor(props){
    super(props);
    this.state=
    {
        users:[],
        email: '',
        expiration_date: '',
        id: 0
    }
}

componentDidMount(){
    axios.get("http://192.168.0.21:5000/users")
    .then((res) => 
    this.setState({ 
        users: res.data.users,
        email: '',
        expiration_date: '',
        id: 0
    }, () => {
        console.log(this.state.users);})
    )
}

emailchange = event =>{
    this.setState({
        email:event.target.value
    })
}

datechange = event =>{
    this.setState({
        expiration_date:event.target.value
    })
}

submit(event,id){
    const headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin":"*",
        "Access-Control-Allow-Headers":"*"
      };
    console.log('before', this.expiration_date)
    const params = {
        "email": "gugucastro56@gmail.com", 
        "expiration_date": "2022-03-12"
    }
    
    event.preventDefault()
if(id===0){
    axios.post('http://192.168.0.21:5000/users', 
    {
        "email": this.state.email, 
        "expiration_date": this.state.expiration_date
    })
    .then(() => {
        this.componentDidMount();
    })
    .catch(function (error) {
        console.log('err:',error);
    });
}
}
delete(id){
    axios.delete(`http://192.168.0.21:5000/users/${id}`)
    .then(()=>{
        this.componentDidMount()
    })
}
render(){
  return (
    <div className="container mt-5">
        <div className="row mt-5">
            <div className="col lg-6 mt-5">
                <form onSubmit={(e)=>{this.submit(e,this.state.id)}}>
                    <div className="form-group">
                        <input type="email" onChange={(e)=>{this.emailchange(e)}}className="form-control mt-2" placeholder={this.state.email} />
                    </div>
                    <div className="form-group">
                        <input type="date" onChange={(e)=>{this.datechange(e)}}className="form-control mt-2" placeholder={this.state.expiration_date}/>
                    </div>
                    <button className="btn btn-block btn-primary mt-2">Submit</button>
                </form>
            </div>
            <div className="col lg-6 mt-5">
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



                        {this.state.users.map(user=>
                        <tr>
                            <td>{user.email}</td>
                            <td>{user.expiration_date}</td>
                            <td>
                                <button className="btn btn-sm btn-primary">
                                    <i className="fa fa-pencil"></i>
                                </button>
                            </td>
                            <td>
                                <button onClick={(e)=>this.delete(user.id)} className="btn btn-sm btn-danger">
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
