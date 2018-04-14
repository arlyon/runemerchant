import {removeWordAt} from "../src/js/components/TaggedSearchBar";
import {expect} from 'chai';
import * as mocha from 'mocha';

describe('Remove Word At', () => {

    mocha.it('Remove nothing on empty string', () => {
        const {word, newString} = removeWordAt("", 0);
        expect(word).to.equal('');
        expect(newString).to.equal('');
    });

    mocha.it('Remove the first word', () => {
        const {word, newString} = removeWordAt("hello", 0);
        expect(word).to.equal('hello');
        expect(newString).to.equal('');
    });

    mocha.it('Remove the first word', () => {
        const {word, newString} = removeWordAt("hello world", 0);
        expect(word).to.equal('hello');
        expect(newString).to.equal('world');
    });

});