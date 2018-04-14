import * as React from "react";

export const Footer = () =>
    <footer className="bg-primary">
        <section>Links!</section>
        <section id="copyright" className="dark">
            <p>
                Some data used in this app is gathered from <a target="_blank" rel="noopener"
                                                               href="https://www.rsbuddy.com">RSBuddy</a>,
                the <a target="_blank" rel="noopener" href="https://oldschoolrunescape.wikia.com/">Runescape
                Wiki</a>, and
                the <a target="_blank" rel="noopener"
                       href="http://services.runescape.com/m=itemdb_oldschool/">Grand Exchange</a>.
                Other data was manually compiled. All gathered data
                is <a target="_blank" rel="noopener" href="https://www.github.com/arlyon/runemerch">available
                    for download</a>.
            </p>
            <p>
                RuneScape is a registered trademark of Jagex Ltd.
                This website is in no way affiliated with, authorized,
                maintained, sponsored or endorsed by Jagex Ltd or
                any of its affiliates or subsidiaries.
            </p>
            <p>
                Want a feature? Got some ideas? This is a free and open source project by Alexander Lyon.
                The code is available on <a target="_blank" rel="noopener" href="https://www.github.com/arlyon/runemerch">github</a>.
            </p>
        </section>
    </footer>;
