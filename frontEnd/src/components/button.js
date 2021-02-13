import React from "react";
import "./Button.css"
import PianoIcon from "./piano.png";
import axios from "axios";

class Button extends React.Component {
  constructor(props) { /* Parent Component Constructor */
    super(props);
    this.state = {
       showLink : false
    }
 }   
  downloadFile = (link) => {
  window.location.href = link
}
     sendRequest= () => {
        axios.get('http://localhost:5000', {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                    }
    })
    .then(result => {
       
      console.log(result.data.fileLocation); return this.downloadFile(result.data.fileLocation); })
    .catch(error => { console.error(error); return Promise.reject(error); });
    };
    
    render(){
    return ( <div class="container">
        <div class="upCenter">
        <img src={PianoIcon} /> 
        </div>
    
    <       div class="center">
    
      <button onClick={this.sendRequest} >Click here for music </button>
    </div>
  </div>);
}};

export default Button;