import React from 'react';

export interface ISearchProps {
    label?: string;
    placeholder: string
    searchChanged: (text?: string, tags?: string[]) => void
}

interface ISearchState {
    text: string;
    tags: string[];
}

/**
 *
 * @param {string} str
 * @param {number} pos
 * @returns {{word: string; newString: string}}
 */
const removeWordAt = (str: string, pos: number): { word: string, newString: string } => {
    // Search for the word's beginning and end.
    const left = str.slice(0, pos + 1).search(/\S+$/);
    const right = str.slice(pos).search(/\s/);
    const newString = str.substring(0, left) + str.substring(right, -1);

    // The last word in the string is a special case.
    if (right < 0) {
        return {word: str.slice(left), newString,};
    }

    // Return the word, using the located bounds to extract it from the string.
    return {word: str.slice(left, right + pos), newString,};
};

/**
 *
 */
export class TaggedSearchBar extends React.Component<ISearchProps, ISearchState> {

    private input: HTMLInputElement | null = null;

    constructor(props: ISearchProps) {
        super(props);

        const text = localStorage.getItem("search") || "";
        const tagString = localStorage.getItem("tags");
        const tags = tagString ? tagString.split(",") : [];

        this.state = {
            items: [],
            text,
            tags
        } as ISearchState;

        document.addEventListener('keydown', this.handleAddTag);
        document.addEventListener('keydown', this.handleRemoveTag);

        this.props.searchChanged(text, tags);
    }

    /**
     * Handles changes to the input box.
     * @param event The input event.
     */
    private handleChange = async (event: React.FormEvent<HTMLInputElement>) => {
        const text = event.currentTarget.value;
        this.setState({
            text,
        });
        localStorage.setItem("search", text);
        this.props.searchChanged(text);
    };

    /**
     * Checks the keyboard event for whether a tag should be added.
     * @param {KeyboardEvent} event
     */
    private handleAddTag = (event: KeyboardEvent) => {
        if (
            event.code === 'Space' &&
            event.shiftKey &&
            this.input === document.activeElement &&
            this.state.tags.length < 3
        ) {
            const {word, newString} = removeWordAt(this.state.text, this.input.selectionStart);
            if (word === " " || word === "") return;

            const tags = [...this.state.tags, word];
            localStorage.setItem("tags", tags.join(","));
            localStorage.setItem("search", newString);

            this.setState({
                tags,
                text: newString
            });

            this.props.searchChanged(newString, tags);
            event.preventDefault();
        }
    };

    /**
     * Checks the keyboard event for whether a tag should be removed.
     * @param {KeyboardEvent} event
     */
    private handleRemoveTag = (event: KeyboardEvent) => {
        if (
            event.code === 'Backspace' &&
            this.input === document.activeElement &&
            this.input.selectionStart === 0 &&
            this.state.tags.length
        ) {
            const text = event.shiftKey ? "" : this.state.tags[this.state.tags.length - 1] + this.state.text;
            const tags = this.state.tags.slice(0, -1);

            localStorage.setItem("tags", tags.join(","));
            localStorage.setItem("search", text);

            this.setState({
                tags,
                text,
            });

            this.props.searchChanged(text, tags);
            event.preventDefault();
        }
    };

    /**
     * Renders the component.
     * @param {ISearchProps} props
     * @param {{}} state
     * @param context
     * @returns {JSX.Element}
     */
    public render(props?: ISearchProps, state?: {}, context?: any): JSX.Element {

        const tags = this.state.tags.map(
            (tag: string, index: number) => <span key={index} className="tag"><span>{tag}</span></span>
        );

        return (
            <div className="search">
                <div className="tags">
                    {tags}
                </div>
                <input
                    placeholder={this.props.placeholder}
                    onChange={this.handleChange}
                    value={this.state.text}
                    ref={(el) => this.input = el}
                />
            </div>
        );
    }

    componentDidMount() {
        this.input!.focus()
    }

    /**
     * Unregisters the event listeners on unmount.
     */
    componentWillUnmount() {
        document.removeEventListener('keydown', this.handleAddTag);
        document.removeEventListener('keydown', this.handleRemoveTag);
    }
}
