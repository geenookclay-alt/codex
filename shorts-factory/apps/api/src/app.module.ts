import { Module } from '@nestjs/common';
import { AuthModule } from './modules/auth/auth.module';
import { UsersModule } from './modules/users/users.module';
import { TeamsModule } from './modules/teams/teams.module';
import { ChannelsModule } from './modules/channels/channels.module';
import { ProjectsModule } from './modules/projects/projects.module';
import { StrategiesModule } from './modules/strategies/strategies.module';
import { TasksModule } from './modules/tasks/tasks.module';
import { QueueModule } from './modules/queue/queue.module';
import { UploadsModule } from './modules/uploads/uploads.module';
import { AnalyticsModule } from './modules/analytics/analytics.module';
import { RecommendationsModule } from './modules/recommendations/recommendations.module';

@Module({
  imports: [
    AuthModule,
    UsersModule,
    TeamsModule,
    ChannelsModule,
    ProjectsModule,
    StrategiesModule,
    TasksModule,
    QueueModule,
    UploadsModule,
    AnalyticsModule,
    RecommendationsModule
  ]
})
export class AppModule {}
