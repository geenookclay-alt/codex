import { Module } from '@nestjs/common';
import { ChannelPoliciesController } from './channel-policies.controller';
import { ChannelPoliciesService } from './channel-policies.service';

@Module({ controllers: [ChannelPoliciesController], providers: [ChannelPoliciesService] })
export class ChannelPoliciesModule {}
