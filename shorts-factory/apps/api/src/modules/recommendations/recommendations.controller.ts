import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { RecommendationsService } from './recommendations.service';
import { CreateRecommendationsDto } from './dto/create-recommendations.dto';

@Controller('recommendations')
export class RecommendationsController {
  constructor(private readonly service: RecommendationsService) {}

  @Get()
  list() {
    return this.service.list();
  }

  @Get(':id')
  get(@Param('id') id: string) {
    return this.service.get(id);
  }

  @Post()
  create(@Body() body: CreateRecommendationsDto) {
    return this.service.create(body);
  }
}
