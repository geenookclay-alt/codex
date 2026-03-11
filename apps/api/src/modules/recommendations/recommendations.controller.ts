import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { RecommendationsService } from './recommendations.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('recommendations')
@UseGuards(JwtAuthGuard)
export class RecommendationsController {
  constructor(private readonly service: RecommendationsService) {}
  @Get()
  list() { return this.service.list(); }
  @Post()
  upsert(@Body() body: any) { return this.service.upsert(body); }
}
