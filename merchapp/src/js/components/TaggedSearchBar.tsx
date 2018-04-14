import * as React from 'react';

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
 * Removes the occupying the given index from a string.
 * @param {string} str The string to extract the word from.
 * @param {number} pos The character index of the word.
 * @returns {{word: string; newString: string}} An object with the new string and extracted word.
 */
export const removeWordAt = (str: string, pos: number): { word: string, newString: string } => {
    // Search for the word's beginning and end.
    const leftBound = str.slice(0, pos + 1).search(/\S+$/);
    const rightBound = str.slice(pos).search(/\s/);
    const newString = str.substring(0, leftBound) + str.substring(rightBound, -1);

    // The last word in the string is a special case.
    const word = rightBound == -1 ? str.slice(leftBound) : str.slice(leftBound, rightBound + pos);

    // Return the word, using the located bounds to extract it from the string.
    return {word, newString,};
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
            event.code === 'Enter' &&
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
                    title="Item Search"
                />
            </div>
        );
    }

    componentDidMount() {
        this.input!.focus();
        this.input!.setSelectionRange(this.state.text.length, this.state.text.length)
    }

    /**
     * Unregisters the event listeners on unmount.
     */
    componentWillUnmount() {
        document.removeEventListener('keydown', this.handleAddTag);
        document.removeEventListener('keydown', this.handleRemoveTag);
    }
}
