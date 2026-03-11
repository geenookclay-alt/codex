import { Module } from '@nestjs/common';
import { modules } from './generated-modules';

@Module({ imports: [...modules] })
export class DomainModule {}
