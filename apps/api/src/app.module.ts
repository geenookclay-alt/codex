import { Module } from '@nestjs/common';
import { AuthModule } from './modules/auth/auth.module';
import { DomainModule } from './modules/domain.module';

@Module({ imports: [AuthModule, DomainModule] })
export class AppModule {}
