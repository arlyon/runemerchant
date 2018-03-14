import React from 'react';
import ReactDOM from 'react-dom';
import {Route} from "react-router";
import {BrowserRouter as Router, Switch} from "react-router-dom";
import {FourOFour} from "./components/views/404";
import {ItemView} from "./components/views/item";
import {SearchView} from "./components/views/search";

class App extends React.Component<{}, {}> {
    public render() {
        return <Router>
            <Switch>
                <Route exact path="/" component={SearchView}/>
                <Route path="/items/:id" component={ItemView}/>
                <Route component={FourOFour}/>
            </Switch>
        </Router>;
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById("app") as Element,
);
