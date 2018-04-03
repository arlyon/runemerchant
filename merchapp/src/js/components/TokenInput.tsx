import React from 'react';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCheckCircle, faTimesCircle} from '@fortawesome/pro-light-svg-icons';

export interface ITokenInputProps {
    tokenChanged: (token: string | null) => void
    token: string | null
}

export interface ITokenInputState {
    input: string
    valid: boolean
}

const isToken = RegExp('^[0-9a-fA-F]{40}$');

export class TokenInput extends React.Component<ITokenInputProps, ITokenInputState> {

    constructor(props: ITokenInputProps) {
        super(props);

        const input = this.props.token || "";
        const valid = isToken.test(input);

        this.state = {
            input,
            valid,
        };
    }

    public render(props?: {}, state?: {}, context?: any): JSX.Element {
        return (
            <div className={"token " + (this.state.valid && this.state.input ? "valid" : "")}>
                <span className="tag"><span>0x</span></span>
                <input
                    title="Token Input"
                    onChange={this.handleChange}
                    type="text"
                    value={this.state.input}
                    size={44}
                    maxLength={40}
                    pattern="[a-fA-F0-9]+"
                />
                <div className="icon-container" onClick={this.revertToLastValid}>
                    <FontAwesomeIcon icon={this.state.valid ? faCheckCircle : faTimesCircle}/>
                </div>
            </div>
        )
    }

    /**
     * Validity is controlled by the parent. A new token from the parent
     * means that it is recognised as a valid token.
     * @param {ITokenInputProps} newProps
     */
    public componentWillReceiveProps(newProps: ITokenInputProps) {
        console.log(newProps)
        if (newProps.token != this.props.token) {
            this.setState({
                valid: true,
                input: newProps.token || ""
            })
        }
    };

    /**
     * Checks validity of the token and sends valid ones to the parent.
     * @param {React.FormEvent<HTMLInputElement>} event The form event.
     */
    private handleChange = (event: React.FormEvent<HTMLInputElement>) => {
        const token = event.currentTarget.value || null; // if empty set to null

        this.setState({
            input: event.currentTarget.value,
            valid: token == this.props.token,
        });

        if ((isToken.test(token || "") || (token == null)) && token != this.props.token) {
            this.props.tokenChanged(token);
        }
    };

    /**
     * Reverts the input to the last valid token.
     */
    private revertToLastValid = () => {
        if (this.state.input != this.props.token) {
            this.setState({
                input: this.props.token || "",
                valid: true
            })
        }
    };
}

