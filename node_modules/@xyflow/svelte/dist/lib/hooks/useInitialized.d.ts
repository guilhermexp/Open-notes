/// <reference types="svelte" />
/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import type { Readable } from 'svelte/store';
/**
 * Hook for seeing if nodes are initialized
 * @returns - nodesInitialized Writable
 */
export declare function useNodesInitialized(): Readable<boolean>;
/**
 * Hook for seeing if the flow is initialized
 * @returns - initialized Writable
 */
export declare function useInitialized(): Readable<boolean>;
