/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import { SvelteComponentTyped } from "svelte";
declare const __propDef: {
    props: {
        radius?: number | undefined;
        class?: string | undefined;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type DotPatternProps = typeof __propDef.props;
export type DotPatternEvents = typeof __propDef.events;
export type DotPatternSlots = typeof __propDef.slots;
export default class DotPattern extends SvelteComponentTyped<DotPatternProps, DotPatternEvents, DotPatternSlots> {
}
export {};
