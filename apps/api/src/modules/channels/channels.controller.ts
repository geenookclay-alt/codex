import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { ChannelsService } from './channels.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('channels')
@UseGuards(JwtAuthGuard)
export class ChannelsController {
  constructor(private readonly service: ChannelsService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
