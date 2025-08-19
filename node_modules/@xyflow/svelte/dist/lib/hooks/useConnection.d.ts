/// <reference types="svelte" />
/// <reference types=".pnpm/svelte@4.2.1/node_modules/svelte" />
import type { Readable } from 'svelte/store';
import type { ConnectionState } from '@xyflow/system';
/**
 * Hook for receiving the current connection.
 *
 * @public
 * @returns current connection as a readable store
 */
export declare function useConnection(): Readable<ConnectionState>;
