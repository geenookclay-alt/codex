import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { ChannelPoliciesService } from './channel-policies.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('channel-policies')
@UseGuards(JwtAuthGuard)
export class ChannelPoliciesController {
  constructor(private readonly service: ChannelPoliciesService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
