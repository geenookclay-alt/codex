import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { StrategiesService } from './strategies.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('strategies')
@UseGuards(JwtAuthGuard)
export class StrategiesController {
  constructor(private readonly service: StrategiesService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
