import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import AutosList from './components/AutosList';


// nuevo
class App extends Component {
  // nuevo
  constructor() {
  	super();
 	// nuevo
 	this.state ={
 	   autos: []
 	};
  };

  // nuevo
  componentDidMount() {
    this.getAutos();
  };

  getAutos() {
      axios.get(`${process.env.REACT_APP_AUTOS_SERVICE_URL}/autos`)  // nuevo
       .then((res) =>{ this.setState({ autos: res.data.data.autos }); })
       .catch((err) =>{ console.log(err); });
  };

render() {
    return (
        < section className = "section" >
        < div className = "container" >
        < div className = "columns" >
        < div className = "column is-one-third" >
        < br / >
        < h1 className = "title is-1" > Todos los carros < /h1>
        < hr / > < br / >
        < AutosList autos = {this.state.autos}/>
    < /div>
    < /div>
    < /div>
    < /section>
)
    }
};

ReactDOM.render(<App />, document.getElementById('root'));
