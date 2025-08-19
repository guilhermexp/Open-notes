/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import { SvelteComponentTyped } from "svelte";
declare const __propDef: {
    props: Pick<import("../../types").Node<Record<string, unknown>, string>, "id" | "data" | "width" | "height" | "sourcePosition" | "targetPosition" | "selected" | "dragHandle" | "selectable" | "deletable" | "draggable" | "parentId"> & Required<Pick<import("../../types").Node<Record<string, unknown>, string>, "type" | "dragging" | "zIndex">> & {
        isConnectable: boolean;
        positionAbsoluteX: number;
        positionAbsoluteY: number;
    } & {
        type: any;
    };
    events: {
        [evt: string]: CustomEvent<any>;
    };
    slots: {};
};
export type DefaultNodeProps = typeof __propDef.props;
export type DefaultNodeEvents = typeof __propDef.events;
export type DefaultNodeSlots = typeof __propDef.slots;
export default class DefaultNode extends SvelteComponentTyped<DefaultNodeProps, DefaultNodeEvents, DefaultNodeSlots> {
}
export {};
