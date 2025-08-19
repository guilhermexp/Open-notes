/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import { SvelteComponentTyped } from "svelte";
import type { ZoomProps } from './types';
declare const __propDef: {
    props: ZoomProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {};
    };
};
type ZoomProps_ = typeof __propDef.props;
export { ZoomProps_ as ZoomProps };
export type ZoomEvents = typeof __propDef.events;
export type ZoomSlots = typeof __propDef.slots;
export default class Zoom extends SvelteComponentTyped<ZoomProps_, ZoomEvents, ZoomSlots> {
}
