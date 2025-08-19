/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import { SvelteComponentTyped } from "svelte";
import type { ControlButtonProps } from './types';
declare const __propDef: {
    props: ControlButtonProps;
    events: {
        click: MouseEvent;
    } & {
        [evt: string]: CustomEvent<any>;
    };
    slots: {
        default: {
            class: string;
        };
    };
};
type ControlButtonProps_ = typeof __propDef.props;
export { ControlButtonProps_ as ControlButtonProps };
export type ControlButtonEvents = typeof __propDef.events;
export type ControlButtonSlots = typeof __propDef.slots;
export default class ControlButton extends SvelteComponentTyped<ControlButtonProps_, ControlButtonEvents, ControlButtonSlots> {
}
