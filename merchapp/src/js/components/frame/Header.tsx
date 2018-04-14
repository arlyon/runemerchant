import * as React from "react";
import {Link} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faKey} from '@fortawesome/pro-light-svg-icons';
import {store} from "../../store"
import {observer} from "mobx-react"

export interface IHeaderProps {
    image: string;
    name: string;
}

@observer
export class Header extends React.Component<IHeaderProps, { width: number }> {

    constructor(props: IHeaderProps) {
        super(props);
        this.state = {width: window.innerWidth}
    }

    public render() {
        return (
            <nav className="toolbar">
                <div className="container title">
                    <Link to="/" className="logo">
                        <img src={this.props.image} alt="logo"/>
                        {this.state.width > 600 ? this.props.name : "RM"}
                    </Link>
                    <div className="right">
                        {store.token && <Link to="/dash/" className="bold vertical-align">dashboard</Link>}
                        <Link to="/token/" className={"bold vertical-align token"}>
                            api token
                            <FontAwesomeIcon className={store.token ? "valid" : ""} style={{margin: '0.1em 0 0 0.3em'}}
                                             icon={faKey}/>
                        </Link>
                    </div>
                </div>
            </nav>
        )
    }

    public componentDidMount() {
        this.updateWindowWidth();
        window.addEventListener('resize', this.updateWindowWidth);
    }

    public componentWillUnmount() {
        window.removeEventListener('resize', this.updateWindowWidth);
    }

    private updateWindowWidth = () => {
        this.setState({width: window.innerWidth})
    }
}
