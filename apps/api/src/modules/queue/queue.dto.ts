export class UpsertQueueDto {
  id?: string;
  payload!: Record<string, unknown>;
}
