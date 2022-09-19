import React, { useState, useContext } from "react";
import axios from "axios";
var [token] = ''

const Login = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    
    const submitLogin = (async () => {
      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: { 
          login: email,
          password: password
        }
      };
  
      const response = await axios.post("http://192.168.0.21:5000/login", 
      { 
        login: email,
        password: password
      }).catch(function (error) {
        console.log('err:', error)
        });
      if (response.status === 200) {
        token = response.data.access_token;
      } else {
        console.log('error')
        // setErrorMessage(data.detail);
      }
      access_token = token
      console.log(access_token)
    });

    const handleSubmit = (e) => {
      e.preventDefault();
      submitLogin();
    };
    
    return (
        
      <div className="container">
        <form className="box text-center" onSubmit={handleSubmit}>
          <h3 className="title text-center">Login</h3>
          <div className="field text-center mt-2">
            <label className="label">Usuário</label>
            <div className="control">
              <input
                type="text"
                placeholder="Usuário"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
                value={password}
                onChange={(e) => setPassword(e.target.value)}
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
    );
  };
  export var access_token = token
  export default Login;