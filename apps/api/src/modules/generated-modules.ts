import { UsersModule } from './users/users.module';
import { TeamsModule } from './teams/teams.module';
import { ChannelsModule } from './channels/channels.module';
import { AssetsModule } from './assets/assets.module';
import { ProjectsModule } from './projects/projects.module';
import { StrategiesModule } from './strategies/strategies.module';
import { TasksModule } from './tasks/tasks.module';
import { QueueModule } from './queue/queue.module';
import { UploadsModule } from './uploads/uploads.module';
import { AnalyticsModule } from './analytics/analytics.module';
import { RecommendationsModule } from './recommendations/recommendations.module';
import { ChannelPoliciesModule } from './channel-policies/channel-policies.module';

export const modules = [UsersModule,TeamsModule,ChannelsModule,AssetsModule,ProjectsModule,StrategiesModule,TasksModule,QueueModule,UploadsModule,AnalyticsModule,RecommendationsModule,ChannelPoliciesModule];
