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

export interface RemovedWord {
    word: string,
    newString: string
}

/**
 * Removes the occupying the given index from a string.
 * @param {string} str The string to extract the word from.
 * @param {number} pos The character index of the word.
 * @returns {RemovedWord} An object with the new string and extracted word.
 */
export const removeWordAt = (str: string, pos: number): RemovedWord => {

    // set the left bound to either the first index of the word
    // or the current index if a word cannot be found (-1)
    let leftBound = str.slice(0, pos).search(/\S+$/);
    if (leftBound == -1) leftBound = pos;

    // set the right bound to the last index of the word or to
    // the length of the string if a word cannot be found (-1)
    let rightBound = str.slice(pos).search(/\s/);
    rightBound = rightBound == -1 ? str.length : rightBound + pos;

    // handle trimming the right part to remove redundant spaces
    const leftNewString = str.slice(0, leftBound);
    const rightNewString = leftNewString == "" ? str.slice(rightBound).trimLeft() : str.slice(rightBound);

    return {
        word: str.slice(leftBound, rightBound),
        newString: leftNewString + rightNewString,
    };
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
            this.input.selectionEnd === 0 &&
            this.state.tags.length
        ) {

            let text = this.state.text;
            const tags = this.state.tags.slice(0, -1);

            if (!event.shiftKey) {
                text = this.state.tags[this.state.tags.length - 1] + // last tag
                    (text.length && text[0] != " " ? " " : "") + text; // text with space
            }

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
