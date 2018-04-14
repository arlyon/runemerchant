import {removeWordAt} from "../src/js/components/TaggedSearchBar";
import {expect} from 'chai';
import * as mocha from 'mocha';

describe('Remove Word At', () => {

    mocha.it('should do nothing on empty string', () => {
        const {word, newString} = removeWordAt("", 0);
        expect(word).to.equal('');
        expect(newString).to.equal('');
    });

    mocha.it('should remove a word when at the left boundary', () => {
        const {word, newString} = removeWordAt("hello", 0);
        expect(word).to.equal('hello');
        expect(newString).to.equal('');
    });

    mocha.it('should remove a word when between boundaries', () => {
        const {word, newString} = removeWordAt("hello", 3);
        expect(word).to.equal('hello');
        expect(newString).to.equal('');
    });

    mocha.it('should remove a word when at the right boundary', () => {
        const {word, newString} = removeWordAt("hello", 5);
        expect(word).to.equal('hello');
        expect(newString).to.equal('');
    });

    mocha.it('should remove only the first word at the left boundary', () => {
        const {word, newString} = removeWordAt("hello world", 0);
        expect(word).to.equal('hello');
        expect(newString).to.equal('world');
    });

    mocha.it('should remove only the first word between boundaries', () => {
        const {word, newString} = removeWordAt("hello world", 3);
        expect(word).to.equal('hello');
        expect(newString).to.equal('world');
    });

    mocha.it('should remove only the first word at the right boundary', () => {
        const {word, newString} = removeWordAt("hello world", 5);
        expect(word).to.equal('hello');
        expect(newString).to.equal('world');
    });

    mocha.it('should remove only the second word at the left boundary', () => {
        const {word, newString} = removeWordAt("hello world", 6);
        expect(word).to.equal('world');
        expect(newString).to.equal('hello ');
    });

    mocha.it('should remove only the second word between boundaries', () => {
        const {word, newString} = removeWordAt("hello world", 8);
        expect(word).to.equal('world');
        expect(newString).to.equal('hello ');
    });

    mocha.it('should remove only the second word at the right boundary', () => {
        const {word, newString} = removeWordAt("hello world", 11);
        expect(word).to.equal('world');
        expect(newString).to.equal('hello ');
    });

    mocha.it('should detect numbers', () => {
        const {word, newString} = removeWordAt("1234", 2);
        expect(word).to.equal('1234');
        expect(newString).to.equal('');
    });

    mocha.it('should remove nothing between words', () => {
        const {word, newString} = removeWordAt("two  words", 4);
        expect(word).to.equal('');
        expect(newString).to.equal('two  words');
    });

});