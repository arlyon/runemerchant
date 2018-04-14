import React from 'react';
import {Footer} from "../components/frame/Footer";
import {Header} from "../components/frame/Header";
import {observer} from "mobx-react"

@observer
export class DashboardView extends React.Component<{}, {}> {

    public render(props?: {}, state?: {}, context?: any): JSX.Element {

        return (
            <div id="root">
                <Header name="RuneMerchant" image="/logo_black.svg"/>
                <main className="container">
                    <h1>yeboi</h1>
                </main>
                <Footer/>
            </div>
        );
    }
}
