import React from 'react';
import ReactDOM from 'react-dom';
import {Route} from "react-router";
import {BrowserRouter as Router, Switch} from "react-router-dom";
import {FourOFour} from "./views/404View";
import {ItemView} from "./views/ItemView";
import {SearchView} from "./views/SearchView";

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
