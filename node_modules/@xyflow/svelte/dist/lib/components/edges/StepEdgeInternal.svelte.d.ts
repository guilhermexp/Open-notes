/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import { SvelteComponentTyped } from "svelte";
import type { EdgeProps } from '../../types';
declare const __propDef: {
    props: EdgeProps;
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type StepEdgeInternalProps = typeof __propDef.props;
export type StepEdgeInternalEvents = typeof __propDef.events;
export type StepEdgeInternalSlots = typeof __propDef.slots;
export default class StepEdgeInternal extends SvelteComponentTyped<StepEdgeInternalProps, StepEdgeInternalEvents, StepEdgeInternalSlots> {
}
export {};
